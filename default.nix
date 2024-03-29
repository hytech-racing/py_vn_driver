{ lib
, python311Packages
, asyncudp_pkg
, hytech_np_proto_py
, vn_protos_np_proto_py
, py_vn_lib
}:

python311Packages.buildPythonApplication {
  pname = "vn_udp_driver_pkg";
  version = "1.0.0";
  propagatedBuildInputs = [
    asyncudp_pkg
    python311Packages.protobuf
    hytech_np_proto_py
    vn_protos_np_proto_py
    py_vn_lib
  ];

  src = ./.;
}