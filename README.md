# Weather Resource

Implements a resource that reports when the weather changes. The resource
can detect new forecasts, or just when the current weather has changed.

This resource is powered by [Yahoo! Weather](https://developer.yahoo.com/weather/)

<a href="https://www.yahoo.com/?ilc=401" target="_blank"> <img src="https://poweredby.yahoo.com/purple.png" width="134" height="29"/> </a>

## Source Configuration

* `city`: The city used for the weather forecast. Valid values will look
like `Paris, France` or `boulder, co`. To check whether your city will be
recognized by Yahoo, use their YQL API, and try the following request
`select * from geo.places where text="YOUR CITY NAME"` in their 
[online console](https://developer.yahoo.com/yql/).

* `weather_change_only`: *Optional. Default `false`.* wether the resource
should create new versions only when the weather changes, as opposed to
when a new forecast is released.

## Behavior

### `check`: Produce current weather conditions.

Returns current weather.

### `in`: Report the given time.

Fetches the current weather, writing the value in two separate files in
the destination:

- `weather.txt`: Short message describing the weather, e.g. "Mostly Cloudy"
- `weather.json`: JSON object, containing the `weather` as described above,
as well as the `date` of the forecast:

```json
{
    "weather": "Scattered Snow Showers",
    "date": "Wed, 23 May 2018 02:34 PM CEST"
}
```

#### Parameters

*None.*


### `out`: Produce the current time.

Just don't.

#### Parameters

*None.*


## Examples

### Periodic trigger

```yaml
resource_types:
- name: weather
  type: docker-image
  source:
    repository: kehrlann/weather-resource

resources:
- name: budapest-weather
  type: weather
  source:
    city: Budapest, HU
    weather_change_only: true

jobs:
- name: something-when-the-weather-changes
  plan:
  - get: budapest-weather
    trigger: true
  - task: look-out-the-window
    config: # ...
```

## Development

### Prerequisites

* python is *required* - version 3.6.x is tested.
* docker is *required* - version 18.03.x is tested; earlier versions may work.
* pip is used for dependency management - just installing `requests`
* virtualenv is heavily encouraged, but not mandatory.

### Bootstraping / creating your environment

There is a bootstrap script that will create a venv and install `requests`. To
run it, just:

```sh
./bootstrap.sh
```

If you do not wish to use a virtualenv, a standard pip install should do:

```sh
pip3 install requests
```

### Running the tests locally

The tests are in the test module, under `src`. To run them, simply:

```sh
cd src
python -m unittest
```

If you are using a virtualenv as described above, you can also use a script
to watch your files and re-run the tests when changes are detected:

```sh
./watch_tests.sh
```

### Running the tests on build

The tests have been embedded with the `Dockerfile`; ensuring that the testing
environment is consistent across any `docker` enabled platform. When the docker
image builds, the test are run inside the docker container, on failure they
will stop the build.

Run the tests with the following command:

```sh
docker build -t weather-resource .
```

### Contributing

Please make all pull requests to the `master` branch and ensure tests pass
locally.