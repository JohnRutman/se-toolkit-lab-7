# Web development

<h2>Table of contents</h2>

- [Web server and web client](#web-server-and-web-client)
  - [Web server](#web-server)
  - [Web client](#web-client)
- [Backend](#backend)
- [Frontend](#frontend)
- [Service](#service)
- [Feature flag](#feature-flag)
- [HTML](#html)
- [CSS](#css)
- [JavaScript](#javascript)
- [CDN](#cdn)
- [Troubleshooting](#troubleshooting)
  - [Service is running but a request fails](#service-is-running-but-a-request-fails)

## Web server and web client

### Web server

A web server is software that delivers content or services to [web clients](#web-client) over the [Internet](./computer-networks.md#internet) using a [protocol](./computer-networks.md#protocol).

> [!NOTE]
> We refer to a web server as software only.
>
> Other sources may refer to it as hardware too.
>
> Example: [What is a web server](https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_web_server).

### Web client

A web client is software that requests content from a [web server](#web-server) and displays the received content.

Web clients include browsers (`Chrome`, `Firefox`) and command-line tools ([`curl`](./useful-programs.md#curl)).

## Backend

<!-- TODO -->

## Frontend

<!-- TODO -->

## Service

A service is an application (or part of a system) that exposes endpoints and performs a focused responsibility.

Examples:

- Course materials service.
- Authentication service.
- Recommendation service.

A service can call other services over the network, but to the client it still appears as endpoints that return responses.

## Feature flag

A feature flag (also called a feature toggle) is a mechanism that enables or disables a feature at runtime without deploying new code. Feature flags let teams decouple deployment from release, enabling gradual rollouts, `A/B` testing, and quick rollbacks.

## HTML

`HTML` (`HyperText Markup Language`) is the standard language for structuring content on the web. An `HTML` file defines the structure and content of a web page using tags.

## CSS

`CSS` (`Cascading Style Sheets`) is a language for styling `HTML` content — controlling layout, colors, fonts, and other visual properties.

## JavaScript

`JavaScript` is a programming language that runs in the browser and makes web pages interactive. It can update content, respond to events, and communicate with servers.

## CDN

A `CDN` (`Content Delivery Network`) is a network of distributed servers that delivers static files (such as `HTML`, `CSS`, and `JavaScript`) to users from a location close to them. Serving files from a `CDN` reduces load on the origin server and improves response time.

## Troubleshooting

### Service is running but a request fails

Verify both:

1. The process is listening on the expected port.
2. You are using the correct host and port in your request.
