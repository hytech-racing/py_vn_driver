{ lib
, python311Packages
, py_vn_lib
}:

python311Packages.buildPythonPackage {
  pname = "vn_driver_py";
  version = "1.0.1";

  propagatedBuildInputs = [
    py_vn_lib
  ];

  src = ./.;
}
