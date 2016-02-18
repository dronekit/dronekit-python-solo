from dronekit import connect, VehicleMode
from dronekit.test import with_sitl
from dronekit_solo import SoloVehicle

from nose.tools import assert_equals

@with_sitl
def test_attribute_listener(connpath):
    '''check if the attribute listener api is up to date'''
    v = connect(connpath, wait_ready=True, vehicle_class=SoloVehicle)
    random_value = 123

    def on_gopro_status(vehicle, attribute, value):
        assert_equals(value, random_value)

    v.add_attribute_listener('GOPRO_STATUS', on_gopro_status)
    # manually notify the attribute listenr
    v.notify_attribute_listeners('GOPRO_STATUS', random_value)
