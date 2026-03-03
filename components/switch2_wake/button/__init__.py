import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button
from esphome.const import CONF_ID

from .. import switch2_wake_ns, Switch2WakeComponent

DEPENDENCIES = ["switch2_wake"]

CONF_SWITCH2_WAKE_ID = "switch2_wake_id"

Switch2WakeBurstButton = switch2_wake_ns.class_("Switch2WakeBurstButton", button.Button)

CONFIG_SCHEMA = button.button_schema(Switch2WakeBurstButton).extend(
    {
        cv.GenerateID(CONF_SWITCH2_WAKE_ID): cv.use_id(Switch2WakeComponent),
    }
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await button.register_button(var, config)
    parent = await cg.get_variable(config[CONF_SWITCH2_WAKE_ID])
    cg.add(var.set_parent(parent))

