# INT4 W4A8 for Forge Neo
# The activation path of INT4 ConvRot checkpoints: only the convrot_w4a4 weights change, the setting picks INT8 or
# the checkpoint's own value back.

import dataclasses
from unittest import mock

import torch

import lib_int4_w4a8 as int4


@dataclasses.dataclass(frozen=True)
class Params:
    linear_dtype: str = "int4"


def linear(layout=int4.LAYOUT, linear_dtype="int4"):
    module = torch.nn.Linear(4, 4)
    # stands in for comfy-kitchen's QuantizedTensor: the layout name and frozen params on the weight
    module.weight._layout_cls = layout
    module.weight._params = Params(linear_dtype)
    return module


def model():
    return torch.nn.Sequential(linear(), linear(), linear(layout="TensorWiseINT8Layout"), torch.nn.LayerNorm(4))


def dtypes(net):
    return [m.weight._params.linear_dtype for m in net if hasattr(m.weight, "_params")]


def test_int8_by_default():
    net = model()
    assert int4.apply(net) == 2
    assert dtypes(net) == ["int8", "int8", "int4"]
    # applied again: nothing left to change
    assert int4.apply(net) == 0


def test_as_stored_restores_the_checkpoint_value():
    net = model()
    int4.apply(net)
    with mock.patch.object(int4, "choice", return_value=int4.STORED):
        assert int4.apply(net) == 2
    assert dtypes(net) == ["int4", "int4", "int4"]


def test_a_checkpoint_asking_for_int8_stays_int8():
    net = torch.nn.Sequential(linear(linear_dtype="int8"))
    with mock.patch.object(int4, "choice", return_value=int4.STORED):
        assert int4.apply(net) == 0
    assert dtypes(net) == ["int8"]


def test_only_the_first_step_applies():
    with mock.patch.object(int4, "_diffusion_model", return_value=model()) as found:
        int4.on_cfg_denoiser(mock.Mock(denoiser=mock.Mock(step=3)))
        found.assert_not_called()
        int4.on_cfg_denoiser(mock.Mock(denoiser=mock.Mock(step=0)))
        found.assert_called_once()
