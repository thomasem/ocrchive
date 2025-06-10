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
