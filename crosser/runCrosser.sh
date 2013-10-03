#!/bin/bash

java -cp crosser/Crosser-*.jar -Dlogback.configurationFile=./crosser/logback.xml org.tearne.Crosser "$@"
