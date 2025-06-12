# OCRchive

Document archive that provides OCR processing of documents and full-text search
through a simple web interface.

## Features (Planned)

- Document storage
- OCR processing
- Full-text search (CLI and Web)

## Running Development Stack

Simple. Just run `make dev` for an easy development stack. If you wish to
modify the variables in the resulting `.env` file, edit them and run
`make dev-reset; make dev`.

## Docker Images

Dockerfiles are located in the `dockerfiles/` directory. When building these
be sure to use a build context at the root of the project to make sure all
project references work as expected.

For example, if I wanted to build the API Dockerfile, I would run:
```
docker build -t ocrchive-api -f dockerfiles/api/Dockerfile .
```

## Adding Documents

Currently, you can add documents via `curl` like so:

```bash
curl -X POST -F 'file=@/path/to/file' http://localhost:8000/documents
```

### Example

```text
$ curl -X POST -F 'file=@/home/thomasem/image.png' http://localhost:8000/documents
{"filename":"image.png","size":115144}
```
