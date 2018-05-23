import json
import sys
from datetime import datetime
from typing import List, Union

import weather.yahoo_weather as yahoo_weather
from weather.models import (EmptyVersion, Source, TVersion, Version,
                            load_source_version)


def run_check(source: Source, previous_version: TVersion = EmptyVersion()) -> List[Version]:
    new_version = yahoo_weather.fetch(source)

    if new_version.weather == previous_version.weather:
        return []

    return [new_version]


def output_versions(versions: List[Version]) -> None:
    versions_dict = [v.to_dict() for v in versions]
    print(json.dumps(versions_dict))


if __name__ == "__main__":
    source, version = load_source_version(sys.stdin.read())
    new_versions = run_check(source, version)
    output_versions(new_versions)
