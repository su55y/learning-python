#!/bin/sh
flask --app flaskr db init &&\
    flask --app flaskr db migrate &&\
    flask --app flaskr db upgrade
