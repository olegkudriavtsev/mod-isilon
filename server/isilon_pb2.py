# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: isilon.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='isilon.proto',
  package='server',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0cisilon.proto\x12\x06server\"$\n\x0bInfoRequest\x12\x15\n\rCredentialsId\x18\x01 \x01(\t\"\x1f\n\x0cInfoResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2=\n\x06Isilon\x12\x33\n\x04Info\x12\x13.server.InfoRequest\x1a\x14.server.InfoResponse\"\x00\x62\x06proto3')
)




_INFOREQUEST = _descriptor.Descriptor(
  name='InfoRequest',
  full_name='server.InfoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='CredentialsId', full_name='server.InfoRequest.CredentialsId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=60,
)


_INFORESPONSE = _descriptor.Descriptor(
  name='InfoResponse',
  full_name='server.InfoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='server.InfoResponse.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=93,
)

DESCRIPTOR.message_types_by_name['InfoRequest'] = _INFOREQUEST
DESCRIPTOR.message_types_by_name['InfoResponse'] = _INFORESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

InfoRequest = _reflection.GeneratedProtocolMessageType('InfoRequest', (_message.Message,), {
  'DESCRIPTOR' : _INFOREQUEST,
  '__module__' : 'isilon_pb2'
  # @@protoc_insertion_point(class_scope:server.InfoRequest)
  })
_sym_db.RegisterMessage(InfoRequest)

InfoResponse = _reflection.GeneratedProtocolMessageType('InfoResponse', (_message.Message,), {
  'DESCRIPTOR' : _INFORESPONSE,
  '__module__' : 'isilon_pb2'
  # @@protoc_insertion_point(class_scope:server.InfoResponse)
  })
_sym_db.RegisterMessage(InfoResponse)



_ISILON = _descriptor.ServiceDescriptor(
  name='Isilon',
  full_name='server.Isilon',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=95,
  serialized_end=156,
  methods=[
  _descriptor.MethodDescriptor(
    name='Info',
    full_name='server.Isilon.Info',
    index=0,
    containing_service=None,
    input_type=_INFOREQUEST,
    output_type=_INFORESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_ISILON)

DESCRIPTOR.services_by_name['Isilon'] = _ISILON

# @@protoc_insertion_point(module_scope)
