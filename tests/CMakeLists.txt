ADD_SUBDIRECTORY (unit)
ADD_SUBDIRECTORY (long)
ADD_CUSTOM_TARGET(coverage nosetests-3.4 --verbose
                                         --with-coverage
                                         --cover-package=rpg
                                          -w ${PROJECT_SOURCE_DIR}
                           ${PROJECT_SOURCE_DIR}/tests/unit
                           ${PROJECT_SOURCE_DIR}/tests/long)