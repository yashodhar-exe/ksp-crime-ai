# KSP Datathon Submission: Intelligent Crime Analysis Platform

This project is submitted for the **Karnataka State Police (KSP) Datathon**. It presents a prototype for an intelligent, conversational AI platform designed to empower the State Crime Records Bureau (SCRB) and local investigators.

## Problem Statement

Currently, the SCRB manages crime data from over 1,100 police stations across Karnataka. However, officers often rely on static dashboards and manual database queries, which limits their ability to conduct deep analysis, uncover hidden criminal networks, or receive early-warning signals for emerging crime hotspots.

## Our Solution

This prototype builds a modern conversational AI layer and advanced analytics suite directly on top of structured crime records. It enables investigators to move beyond static reporting and into proactive, intelligence-driven policing.

### Key Capabilities Developed for the Datathon:

1. **Natural Language Querying (NLP)**: Investigators can query complex crime data using plain English, bypassing the need for complex SQL queries or filtering tools.
2. **Criminal Network Visualization**: An interactive radial graph automatically maps and visualizes known relationships between suspects, victims, and associates.
3. **Automated Similar-Case Detection**: The system surfaces historically similar cases based on crime types and Modus Operandi (MO) pattern matching.
4. **Crime Trend & Hotspot Detection**: District-level analytics to highlight emerging crime trends.
5. **Role-Based Access Control**: Secure, tiered access designed around real police hierarchy (Admin, SP, DSP, Inspector, Sub Inspector, Constable).

## Architecture & Technology Stack

Our platform is a fully functional web application, structured as a monorepo for seamless deployment.

- **Backend (API Layer)**: Python & FastAPI
- **Database**: PostgreSQL (handling relational data for citizens, cases, evidence, and audit logs)
- **Frontend (UI Layer)**: React, TypeScript, and Tailwind CSS (packaged via Vite)
- **Deployment Strategy**: Docker & Docker Compose (or Serverless deployment via Zoho Catalyst AppSail & Slate)

## Getting Started

### Prerequisites
- Docker & Docker Compose installed on your machine.
- A local `.env` file (you can copy from `.env.example`).

### Running Locally

```bash
docker compose up -d --build
```
Once the containers are running:
- **Frontend App**: `http://localhost:3000`
- **Backend API Docs**: `http://localhost:8000/docs`

### Demo Accounts

The platform includes role-based access control. You can test the platform using the following demo accounts:

| Username | Role | Password |
|---|---|---|
| `admin.scrb` | Admin | `Demo@KSP2026` |
| `sp.blr.city` | SP | `Demo@KSP2026` |
| `dsp.mysuru` | DSP | `Demo@KSP2026` |

*Note: These are mock accounts generated specifically for the datathon prototype evaluation.*

## Future Roadmap

While this prototype demonstrates significant value, future iterations would include:
- **Kannada Language Support**: Full localization for regional investigators.
- **Advanced Machine Learning**: Upgrading the similar-case detection from pattern matching to a trained NLP embedding model.
- **Geospatial Mapping**: Granular, GPS-based hotspot mapping overlaid on interactive maps.
