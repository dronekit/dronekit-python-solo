from dronekit import connect, VehicleMode
from dronekit.test import with_sitl
from dronekit_solo import SoloVehicle

from nose.tools import assert_equals

class FakeGoproState:
    def __init__(self, cmd_id, status, value):
        self.cmd_id = cmd_id
        self.status = status
        self.value = value

class FakeGoproResponse:
    def __init__(self, cmd_id, status):
        self.cmd_id = cmd_id
        self.status = status

@with_sitl
def test_gopro_state(connpath):
    v = connect(connpath, wait_ready=True, vehicle_class=SoloVehicle)

    fake_gopro_state = FakeGoproState(123, 1, [1, 1, 1, 1])

    def on_gopro_status(vehicle, attribute, value):
        assert_equals(vehicle.gopro_status, value)
        assert_equals(value.cmd_id, fake_gopro_state.cmd_id)
        assert_equals(value.status, fake_gopro_state.status)
        assert_equals(value.value, fake_gopro_state.value)

    v.add_attribute_listener('gopro_status', on_gopro_status)

    # manually notify the attribute listenr
    v.notify_message_listeners('GOPRO_HEARTBEAT', fake_gopro_state)

@with_sitl
def test_gopro_set_response(connpath):
    v = connect(connpath, wait_ready=True, vehicle_class=SoloVehicle)

    fake_gopro_response = FakeGoproResponse(123, 456)

    def on_gopro_set_response(vehicle, attribute, value):
        assert_equals(value[0], fake_gopro_response.cmd_id)
        assert_equals(value[1], fake_gopro_response.status)

    v.add_attribute_listener('gopro_set_response', on_gopro_set_response)

    # manually notify the attribute listenr
    v.notify_message_listeners('GOPRO_SET_RESPONSE', fake_gopro_response)
