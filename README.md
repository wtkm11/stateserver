# State Server!

## How to run with Docker

1. Navigate to the project root directory (the directory with the `Dockerfile`)
   and build an image.

   ```
   $ docker build -t stateserver:latest .
   ```

2. Start a container with stateserver running inside it. Expose port 8080.

   ```
   $ docker run -d -p 8080:8080 stateserver
   ```

3. Post a latitude and longitude to `/` find out which state it is in.

   ```
   $ curl -d "longitude=-77.036133&latitude=40.513799" http://localhost:8080/
   ["Pennsylvania"]
   ```
