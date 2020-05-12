#!/bin/bash
echo [ > installed_packages.json
dpkg-query -W -f '{"name":"${binary:Package}","version":"${Version}"},\n' >> installed_packages.json
echo ] >> installed_packages.json
