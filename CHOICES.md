# CHOICES.md

# Engineering Choices and Decisions

## Overview

This project was built with the goal of creating a practical and understandable retail intelligence system rather than an overly complex research prototype.

Several engineering decisions were made to balance accuracy, implementation speed, and maintainability.

## Why YOLOv8?

YOLOv8 was selected for person detection because it provides a good tradeoff between speed and detection quality.

Retail video analytics requires near real-time performance and stable person detection. YOLOv8 offered:

* strong detection accuracy
* easy integration
* lightweight deployment
* built-in tracking support

More advanced detection pipelines were considered, but they would have increased development complexity without significantly improving challenge requirements.

## Why Tracking IDs Instead of Re-ID?

The system currently uses YOLO tracking IDs to maintain visitor continuity.

A dedicated person Re-ID model could improve cross-camera identity matching, but it introduces additional model complexity and tuning requirements.

For this challenge, tracking IDs were considered sufficient because:

* cameras were processed independently
* implementation time was limited
* event generation accuracy was prioritised

This allowed faster iteration and easier debugging.

## Why Event-Driven Architecture?

An event-driven architecture was chosen because it separates detection from analytics.

Instead of directly calculating metrics inside the vision pipeline, the system emits structured behavioral events.

Benefits include:

* easier debugging
* modular design
* reusable analytics
* simpler future scaling

This also mirrors real-world streaming systems where events act as the interface between services.

## Why JSONL Storage?

JSONL was selected for event storage rather than a database.

The decision was intentional.

During experimentation and debugging, JSONL provided:

* readable logs
* lightweight storage
* simple replay capability
* minimal setup effort

A database could support larger deployments, but JSONL kept development faster and more transparent.

## Why ROI-Based Queue Logic?

Billing queue monitoring was implemented using a rectangular Region of Interest (ROI).

Alternative approaches such as segmentation or pose estimation were considered, but ROI logic was chosen because it is:

* computationally lightweight
* easy to tune
* visually interpretable
* reliable for the provided footage

The queue rectangle could be adjusted quickly during testing to improve counting quality.

## Why FastAPI?

FastAPI was selected for the backend layer.

The project required lightweight APIs capable of exposing analytics quickly.

FastAPI provided:

* fast development
* automatic documentation
* clean routing
* simple integration

This made it suitable for exposing metrics, funnel, anomaly, and conversion endpoints.

## AI-Assisted Development Choices

AI tools were used as development accelerators.

They helped with:

* debugging runtime issues
* refining queue logic
* improving event validation
* structuring documentation

However, AI-generated suggestions were manually reviewed and adapted.

Many changes required practical adjustment to match footage behavior and project architecture.

The final system represents a combination of AI assistance and human engineering decisions.

## Future Engineering Improvements

Future versions of the system could include:

* database-backed event storage
* stronger identity matching
* multi-camera association
* advanced queue prediction
* scalable cloud deployment

These improvements were intentionally deferred to keep the current implementation focused and maintainable.
