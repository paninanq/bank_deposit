#!/bin/bash

psql -U postgres <<-EOSQL
    CREATE DATABASE "deposit";
EOSQL
