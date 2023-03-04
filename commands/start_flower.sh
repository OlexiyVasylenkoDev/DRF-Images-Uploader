#!/bin/bash

celery -A config flower --broker=redis://redis --port=5555