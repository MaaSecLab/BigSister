# Big Sister (OSINT challenge automation tool)

## Description

Big Sister is a collection of script and tools that simplify the process of solving OSINT challenges during CTF competitions. 

## Problem

Open-Source Intelligence (OSINT) challenges are a central part of CTF competitions. They involve giving the participants some data (e.g. Image, Video, Audio etc.) and them finding out more information about the data using context clues and possible file metadata. 

We can automate many of the processes that are common across the majority of OSINT challenges, meaning that we can reduce the amount of time we spend on such challenges, increasing productivity and efficiency.

## Scope

For the first version of our "Big Sister" tool we will implement a metadata scraper and parser, alongside an Image Retrieval and Identification Script (I.R.I.S), which will use pre-existing reverse image search services to find close matches. In later stages we can implement Artificial Intelligence integration, that will provide LLM models such as ChatGPT o3 with the previously gathered data to result in even more comprehensive results.

## Implementation

Our main goal for this project is to create a program that is easy to use and modify. That means that we will use high-level programming languages and scripting languages, such as python, bash and lua. The target Operating System will be Debian-based Linux systems.

The metadata scraper part of the program will make a series of calls to third-party tools, such as exiftool, zsteg, steghide and binwalk. Another part of the program will then parse the output of those tools and store the lines that contain usable information. Lines containing information regarding the name of the user, the location of the file and other custom values are prime targets. Python based operating system calls can make calls to these tools with the file as an argument. Additionally, python is able to handle the parsing by using text matching.

IRIS can also be handled implemented using python. We can fork and use [Google-Reverse-Image-Search unofficial API](https://github.com/RMNCLDYO/Google-Reverse-Image-Search) as the basis for this module.

## Testing

This project will ideally reach a point where it is able to solve challenges without human intervention. We can perform testing by using OSINT challenges from past competitions, we have access to the [ctf-archives repository](https://github.com/sajjadium/ctf-archives) to collect OSINT challenges from a wide variety of competitions.


## Contribuitors
- [Alexia-Madalina Cirstea] (https://github.com/AlexiaMadalinaCirstea) (University emaiL: m.cirstea@student.maastrichtuniversity.nl) (Personal email: mmadalinacirstea@gmail.com)

