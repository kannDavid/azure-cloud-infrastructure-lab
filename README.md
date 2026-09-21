# Azure Cloud Infrastructure & Security Lab

A hands-on Microsoft Azure project designed to simulate a secure cloud environment using networking, identity, private connectivity, containerization, monitoring, logging, and troubleshooting.

The goal of this project was not only to deploy Azure resources, but to understand how they interact and troubleshoot failures across DNS, network security, and access control.

## Technologies Used

- Microsoft Azure
- Microsoft Entra ID
- Azure RBAC
- Azure Virtual Network
- Network Security Groups
- Azure Private Endpoint
- Azure Private DNS
- Azure Blob Storage
- Docker
- Azure Container Registry
- Azure Container Instances
- Azure Monitor
- Log Analytics
- Kusto Query Language (KQL)
- Azure Cost Management

## Architecture

The environment uses the VNet `VN-Lab` with the address space:

`10.10.0.0/16`

It is segmented into six subnets:

| Subnet | Address Space | Purpose |
|---|---|---|
| Clients | 10.10.10.0/24 | Client systems |
| Servers | 10.10.20.0/24 | Server resources |
| Management | 10.10.30.0/24 | Management resources |
| Applications | 10.10.40.0/24 | Application resources |
| Containers | 10.10.50.0/24 | Azure Container Instances |
| PrivateEndpoints | 10.10.60.0/24 | Azure Private Endpoints |

## Security & Private Connectivity

Azure Blob Storage was configured with public network access disabled.

A Private Endpoint provides private access to Blob Storage through the VNet. Azure Private DNS resolves the Storage Account hostname to its private endpoint address (`10.10.60.4`).

Network Security Groups are used to control traffic between network segments.

Microsoft Entra ID groups and Azure RBAC provide identity-based access control using least-privilege permissions.

## Containerized Application

A Python Flask application was containerized using Docker.

The image was:

1. Built and tested locally.
2. Tagged and pushed to Azure Container Registry.
3. Deployed using Azure Container Instances.
4. Integrated with the Azure virtual network for private connectivity.

The application exposes a `/health` endpoint for testing.

## Monitoring & Logging

Azure Monitor and Log Analytics were configured to provide visibility into the environment.

The lab includes:

- Azure Monitor metrics
- Metric-based alert rules
- Email notifications using an Action Group
- Storage diagnostic settings
- Blob read/write/delete logging
- Log Analytics workspace
- KQL queries for investigating Blob Storage activity
- Azure Activity Log analysis

A monthly Azure Cost Management budget was also configured with spending notifications.

## Troubleshooting Scenarios

Three failures were intentionally introduced and diagnosed.

### 1. Private DNS Failure

The Storage Account's private DNS record was intentionally changed from `10.10.60.4` to an incorrect address.

Troubleshooting included verifying the Private Endpoint, checking DNS resolution, identifying the incorrect A record, correcting it, and validating HTTPS connectivity.

### 2. NSG Blocking HTTPS

An outbound NSG rule was created to deny TCP/443 from the Containers subnet to the Storage Private Endpoint.

DNS continued to resolve correctly, but TCP/443 timed out.

Testing different ports helped isolate the issue to network filtering. The NSG rule was identified and corrected, restoring HTTPS connectivity.

### 3. RBAC Authorization Failure

Blob data access permissions were removed while network connectivity remained operational.

The issue demonstrated the difference between Azure management-plane access and data-plane access.

The `Reader` role allowed visibility into Azure resources and configuration, while `Storage Blob Data Reader` was required to read Blob Storage data.

Access was restored using the least-privilege `Storage Blob Data Reader` role.

## Key Takeaways

This project provided hands-on experience with:

- Designing segmented Azure networks
- Securing cloud resources with NSGs
- Implementing private cloud connectivity
- Understanding DNS in private Azure environments
- Applying least-privilege RBAC
- Containerizing and deploying applications
- Monitoring cloud resources
- Querying operational logs with KQL
- Troubleshooting DNS, TCP connectivity, NSGs, and authorization
- Monitoring cloud spending
