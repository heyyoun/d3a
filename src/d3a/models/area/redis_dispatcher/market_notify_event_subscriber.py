import json
import logging
from concurrent.futures import ThreadPoolExecutor
from d3a.models.market.market_structures import offer_from_JSON_string, trade_from_JSON_string
from d3a.events import MarketEvent
from d3a.models.area.redis_dispatcher.redis_communicator import ResettableCommunicator


class MarketNotifyEventSubscriber:
    """
    Used from the area class, subscribes to the market events and triggers the broadcast_events
    method
    """
    def __init__(self, area, root_dispatcher):
        self.area = area
        self.root_dispatcher = root_dispatcher
        self.redis = ResettableCommunicator()
        self.futures = []
        self.executor = ThreadPoolExecutor(max_workers=10)

    def publish_notify_event_response(self, market_id, event_type, transaction_uuid):
        response_channel = f"market/{market_id}/notify_event/response"
        response_data = json.dumps({"response": event_type.name.lower(),
                                    "event_type_id": event_type.value,
                                    "transaction_uuid": transaction_uuid})
        self.redis.publish(response_channel, response_data)

    def _cleanup_all_running_threads(self):
        for future in self.futures:
            try:
                future.result(timeout=5)
            except Exception as e:
                logging.error(f"future {future} timed out during cleanup. Exception: {str(e)}")
        self.futures = []

    def cycle_market_channels(self):
        self._cleanup_all_running_threads()
        try:
            self.redis.stop_all_threads()
        except Exception as e:
            logging.debug(f"Error when stopping all threads when recycling markets: {str(e)}")
        self.redis = ResettableCommunicator()
        self.subscribe_to_events()

    def subscribe_to_events(self):
        channels_callbacks_dict = {}
        for market in self.area.all_markets:
            channel_name = f"market/{market.id}/notify_event"

            def generate_notify_callback(payload):
                event_type, kwargs = self.parse_market_event_from_event_payload(payload)
                data = json.loads(payload["data"])
                kwargs["market_id"] = market.id

                def executor_func():
                    transaction_uuid = data.pop("transaction_uuid", None)
                    assert transaction_uuid is not None
                    self.root_dispatcher.broadcast_callback(event_type, **kwargs)
                    self.publish_notify_event_response(market.id, event_type, transaction_uuid)

                self.futures.append(self.executor.submit(executor_func))

            channels_callbacks_dict[channel_name] = generate_notify_callback
        self.redis.sub_to_multiple_channels(channels_callbacks_dict)

    def parse_market_event_from_event_payload(self, payload):
        data = json.loads(payload["data"])
        kwargs = data["kwargs"]
        for key in ["offer", "existing_offer", "new_offer"]:
            if key in kwargs:
                kwargs[key] = offer_from_JSON_string(kwargs[key])
        if "trade" in kwargs:
            kwargs["trade"] = trade_from_JSON_string(kwargs["trade"])
        event_type = MarketEvent(data["event_type"])
        return event_type, kwargs