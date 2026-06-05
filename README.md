# Agentic Kubernetes Troubleshooter

An intelligent agent-based framework for automatically identifying and analyzing errors, anomalies, and inefficiencies in Kubernetes deployments and services.

## Overview

This framework uses an agentic architecture where a central agent orchestrates specialized skills to diagnose and debug issues across different layers of a Kubernetes cluster:

- **Compute**: CPU, memory, pod scheduling, node health
- **Storage**: PVC/PV issues, disk space, I/O performance
- **Network**: Service connectivity, ingress/egress, DNS resolution

## Architecture

```
Agent (agent.md)
├── Compute Skill (skills/compute_skill.py)
├── Storage Skill (skills/storage_skill.py)
└── Network Skill (skills/network_skill.py)
```

## Getting Started

1. Configure your Kubernetes cluster access (kubeconfig)
2. Run the agent to scan your cluster
3. Review identified issues and anomalies
4. Use individual skills for deeper analysis

## Project Structure

- `agent.md` - Framework documentation and agent specifications
- `skills/` - Specialized skill implementations
  - `compute_skill.py` - Compute resource analysis
  - `storage_skill.py` - Storage analysis
  - `network_skill.py` - Network analysis
- `config/` - Configuration files
- `utils/` - Utility functions and helpers
