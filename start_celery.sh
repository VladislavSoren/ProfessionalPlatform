#!/bin/bash

cd pro_platform

celery -A pro_platform worker -l INFO