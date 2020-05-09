# JMRI Roster

## What is it?
A simple read-only API and web viewer for a [JMRI roster](https://www.jmri.org/help/en/html/apps/DecoderPro/Roster.shtml).

## Why is it?
I built this because I was tired of having information about my locomotivesk mastered in several places. I decided that, since I was already syncing my JMRI roster to a cloud storage service, it made sense to sync this data back down to a NAS and provide an API that could serve this data to any client over the internet at any time.

## How does it work?
When pointed at a JMRI directory containing `roster.xml` and the associated roster entry files, it will expose a simple REST API that returns either the entire roster, or the details for one particular roster entry.

## What does the API look like?
Since all changes to the roster are made in JMRI, the API is read-only (i.e. you can only GET data - no PUT / POST / UPDATE or DELETE).
The API provides two commands:
### Get roster
```
GET api/v1/roster/
```
This returns a JSON array of objects, with each object representing a locomotive in the roster. This is useful if you want to display a list of locomotives in your application. This command takes no parameters.
### Get locomotive
```
GET api/v1/locomotive/<id>
```
Returns a JSON object containing information about a single locomotive. The `id` parameter is the ID of the locomotive, and corresponds to the `id` field found in each object returned by `GET api/v1/roster`.

## Nice, but why not use onf of the APIs JMRI already provides?
I looked at using both the JMRI JSON and web APIs, and whilst they expose all the information I needed, for the API to be always available it would require JMRI to be always running on a server or NAS. This is totally overkill for serving a simple read-only view of the data!

## What about the GUI you mentioned earlier?
For cases when you just want to view data quickly in a web browser, a simple web UI is also provided. As with the API, there are two components:
### Show roster
```
GET /
```
Browsing to the web root will show a table of all the locomotives in the roster. This table shows only the basic information, such as ID, name, address and a link to details page (see below).
### Show locomotive details
```
GET locomotive/<id>
```
Shows detailed information about a single locomotive. The `id` parameter is the ID of the locomotive, and corresponds to the `id` column found in the roster table .

## Ok this sounds great. How do I install this?
Setup using Docker is simple. Basically all you need to do is to mount your `jmri/data` directory into the container and tell it which port to use for API and web UI access. 
### Docker run
```
docker run -d -p 80:8080 -v /path/to/jmri/data:/var/www/jmri-data tomhomewood/roster:latest
```
* `/path/to/jmri/data` is the path to your JMRI `data` folder (this data folder is the one that contains `roster.xml` and the `roster` directory).
* In the above example the API and UI will be available on port 80 on your Docker host - change this to something else if required.
### Docker compose (recommended)
See [here](docker-compose.yml) for an example compose file. As with the run command, all it requires is the path to the jmri data directory and a port to use.