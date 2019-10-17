# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: isg_ai.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='isg_ai.proto',
  package='isg_ai',
  syntax='proto2',
  serialized_pb=_b('\n\x0cisg_ai.proto\x12\x06isg_ai\"\x8d\x01\n\x0fImageNumberPair\x12\x10\n\x08\x63hannels\x18\x01 \x01(\x05\x12\x12\n\nimg_height\x18\x02 \x01(\x05\x12\x11\n\timg_width\x18\x03 \x01(\x05\x12\r\n\x05image\x18\x04 \x01(\x0c\x12\x0e\n\x06number\x18\x05 \x01(\x0c\x12\x10\n\x08img_type\x18\x06 \x01(\t\x12\x10\n\x08num_type\x18\x07 \x01(\t')
)




_IMAGENUMBERPAIR = _descriptor.Descriptor(
  name='ImageNumberPair',
  full_name='isg_ai.ImageNumberPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='channels', full_name='isg_ai.ImageNumberPair.channels', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='img_height', full_name='isg_ai.ImageNumberPair.img_height', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='img_width', full_name='isg_ai.ImageNumberPair.img_width', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='image', full_name='isg_ai.ImageNumberPair.image', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='number', full_name='isg_ai.ImageNumberPair.number', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='img_type', full_name='isg_ai.ImageNumberPair.img_type', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='num_type', full_name='isg_ai.ImageNumberPair.num_type', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=25,
  serialized_end=166,
)

DESCRIPTOR.message_types_by_name['ImageNumberPair'] = _IMAGENUMBERPAIR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ImageNumberPair = _reflection.GeneratedProtocolMessageType('ImageNumberPair', (_message.Message,), dict(
  DESCRIPTOR = _IMAGENUMBERPAIR,
  __module__ = 'isg_ai_pb2'
  # @@protoc_insertion_point(class_scope:isg_ai.ImageNumberPair)
  ))
_sym_db.RegisterMessage(ImageNumberPair)


# @@protoc_insertion_point(module_scope)