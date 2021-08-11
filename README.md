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

![](https://user-images.githubusercontent.com/25964718/129025190-99be8e5b-b0d9-4826-8606-11c3c5d215cc.png)
![](https://user-images.githubusercontent.com/25964718/129025199-6ab9002c-32d2-41ae-9827-dc1c60295858.png)

## Todo

- [x] Run the program on a simple web server using gradio
- [x] Print the predicted digits
- [x] Print the computed sums
- [x] Add a DOCKERFILE and instructions for how to run it
- [ ] Implement digit classification
- [ ] Improve the grid detection
- [ ] Reduce the image size to a fix size, right now the image processing
  settings are set to match the example image
