import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import esp32_ble
from esphome.const import CONF_ID, CONF_DURATION

CODEOWNERS = []
DEPENDENCIES = ["esp32", "esp32_ble"]
AUTO_LOAD = ["esp32_ble"]

switch2_wake_ns = cg.esphome_ns.namespace("switch2_wake")
Switch2WakeComponent = switch2_wake_ns.class_(
    "Switch2WakeComponent",
    cg.Component,
    cg.Parented.template(esp32_ble.ESP32BLE),
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(Switch2WakeComponent),
        cv.GenerateID(esp32_ble.CONF_BLE_ID): cv.use_id(esp32_ble.ESP32BLE),
        cv.Optional(CONF_DURATION, default="2000ms"): cv.positive_time_period_milliseconds,
        cv.Optional("packet_count", default=500): cv.int_range(min=1, max=2000),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    parent = await cg.get_variable(config[esp32_ble.CONF_BLE_ID])
    esp32_ble.register_gap_event_handler(parent, var)
    cg.add(var.set_parent(parent))
    await cg.register_component(var, config)
    cg.add(var.set_burst_ms(config[CONF_DURATION].total_milliseconds))
    cg.add(var.set_packet_count(config["packet_count"]))
