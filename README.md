# Score scanner

Scan hand-written score boards/score sheets and compute the sum for each column.
Use it with a yahtzee score sheet for example.

## Usage

### Using docker

Run the program as a local web server accessible on
[http://0.0.0.0:8080](http://0.0.0.0:8080).

```sh
docker build -t scorescanner .
docker run -i -t --rm -p 8080:8080 scorescanner
```

## Examples

Using the example image when running the web server, you will get something like this

![](https://user-images.githubusercontent.com/25964718/129023050-78c1bfab-69a9-4e68-862d-7fc301d392b6.png)

## Todo

- [x] Run the program on a simple web server using gradio
- [x] Print the predicted digits
- [x] Print the computed sums
- [x] Add a DOCKERFILE and instructions for how to run it
- [ ] Implement digit classification
- [ ] Improve the grid detection
- [ ] Reduce the image size to a fix size, right now the image processing
  settings are set to match the example image
