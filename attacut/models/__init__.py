import importlib
import re

import torch
import torch.nn as nn

def get_model(model_name):
    module_path = "attacut.models.%s" % model_name
    # todo: using logger
    print("Taking %s" % module_path)
    model_mod = importlib.import_module(module_path)
    return model_mod.Model

class ConvolutionBatchNorm(nn.Module):
    def __init__(self, channels, filters, kernel_size, stride=1, dilation=1):
        super(ConvolutionBatchNorm, self).__init__()

        padding = kernel_size // 2
        padding += padding * (dilation-1)

        self.conv = nn.Conv1d(
            channels,
            filters,
            kernel_size,
            stride=stride,
            dilation=dilation,
            padding=padding
        )

        self.bn = nn.BatchNorm1d(filters)

    def forward(self, x):
        return self.bn(self.conv(x))

class ConvolutionLayer(nn.Module):
    def __init__(self, channels, filters, kernel_size, stride=1, dilation=1):
        super(ConvolutionLayer, self).__init__()

        padding = kernel_size // 2
        padding += padding * (dilation-1)

        self.conv = nn.Conv1d(
            channels,
            filters,
            kernel_size,
            stride=stride,
            dilation=dilation,
            padding=padding
        )

    def forward(self, x):
        return self.conv(x)

class BaseModel(nn.Module):
    @classmethod
    def load(cls, path, data_config, model_config, with_eval=True):
        model = cls(data_config, model_config)

        model_path = "%s/model.pth" % path
        model.load_state_dict(torch.load(model_path, map_location="cpu"))

        print("Loading: %s|%s (variables %d)" % (
            model_path,
            model_config,
            model.total_trainable_params()
        ))

        if with_eval:
            print("setting model to eval mode")
            model.eval()

        return model

    def total_trainable_params(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


class SyllableCharacterBaseModel(BaseModel):
    pass

class SyllableBaseModel(BaseModel):
    pass

class SyllableSeqBaseModel(BaseModel):
    pass

class CharacterSeqBaseModel(BaseModel):
    pass

class CharacterSeqWithChTypeBaseModel(BaseModel):
    pass

class SyllableCharacterSeqBaseModel(BaseModel):
    pass

class SyllableCharacterSeqWithChTypeBaseModel(BaseModel):
    pass