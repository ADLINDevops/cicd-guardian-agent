# CI/CD Guardian Agent 🤖

An AI-powered agent that automatically diagnoses CI/CD pipeline failures 
and creates actionable GitLab issues — so developers spend less time 
debugging and more time shipping.

## The Problem

When a CI pipeline fails, a developer has to:
- Dig through walls of job logs
- Figure out what broke and why
- Manually create a ticket
- Go back and comment on the MR

This takes 20–30 minutes every single time.

## The Solution

CI/CD Guardian Agent does it in seconds:
1. Detects a failed pipeline in GitLab
2. Reads the job log automatically
3. Sends it to Gemini AI for diagnosis
4. Creates a GitLab issue with root cause and fix steps

## Tech Stack

- **Gemini 2.5 Flash** — AI diagnosis engine
- **Google Cloud Agent Builder** — Agent orchestration
- **GitLab MCP Server** — Pipeline and issue integration
- **Python** — Core agent logic

## How It Works
- Failed Pipeline → GitLab API → Gemini AI → Auto-created Issue

## Setup

1. Clone this repo:
```
   git clone https://github.com/ADLINDevops/cicd-guardian-agent.git
   cd cicd-guardian-agent
```
