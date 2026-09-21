# Azure Cloud Lab – Troubleshooting Scenarios

This document covers troubleshooting scenarios intentionally introduced into the Azure environment to practice identifying failures across DNS, network connectivity, security controls, and authorization.

---

## Scenario 1 – Private DNS Misconfiguration

### Problem

The application could no longer correctly reach the Azure Storage Account through its Private Endpoint.

Public network access to the Storage Account remained disabled.

### Investigation

I first verified that the Storage Private Endpoint was deployed and connected.

The Private Endpoint had the private IP:

`10.10.60.4`

I then tested DNS resolution for the Storage Account.

The hostname resolved to:

`10.10.60.99`

This did not match the actual Private Endpoint address.

### Root Cause

The Azure Private DNS A record had been incorrectly configured to point to `10.10.60.99` instead of the Private Endpoint at `10.10.60.4`.

### Resolution

I corrected the Private DNS A record:

`10.10.60.99 → 10.10.60.4`

I then performed another DNS lookup and confirmed that the Storage Account resolved to the correct private address.

HTTPS connectivity to Azure Storage was tested afterward to confirm service reachability.

### Lesson

DNS should be validated separately from network connectivity. A Private Endpoint can be healthy while clients are still unable to reach it because DNS is directing traffic to the wrong address.

---

## Scenario 2 – NSG Blocking HTTPS

### Problem

The application correctly resolved the Storage Account to `10.10.60.4`, but HTTPS connectivity to Blob Storage failed.

### Investigation

DNS resolution was tested first and returned the correct Private Endpoint IP.

TCP connectivity to port 443 was then tested.

`TCP/443 → Timeout`

Testing another port showed that connectivity was not completely unavailable.

This suggested that the problem was related to port-specific traffic filtering rather than DNS.

I inspected the Network Security Group associated with the Containers subnet.

### Root Cause

An outbound NSG rule denied:

- Source: `10.10.50.0/24`
- Destination: `10.10.60.4/32`
- Protocol: TCP
- Destination port: `443`
- Action: Deny
- Priority: `100`

The rule prevented the container from establishing HTTPS connections to the Storage Private Endpoint.

### Resolution

The incorrect deny rule was removed/corrected.

TCP/443 connectivity was tested again to confirm that HTTPS traffic could reach the Storage Private Endpoint.

### Lesson

Troubleshooting connectivity should isolate different layers:

1. Verify DNS resolution.
2. Verify the destination IP.
3. Test the required TCP/UDP port.
4. Inspect NSGs and other security controls.
5. Correct the configuration.
6. Repeat the original test to validate the fix.

---

## Scenario 3 – RBAC Authorization Failure

### Problem

Network connectivity to Azure Storage was operational, but a user did not have the required permission to read Blob Storage data.

### Investigation

The network path was validated first:

- Private DNS resolution was correct.
- The Private Endpoint was healthy.
- TCP/443 connectivity was available.

Because connectivity was functioning, I investigated identity and authorization.

The user inherited the Azure `Reader` role through the `Cloud-Lab-Admins` group.

However, the required `Storage Blob Data Reader` role assignment had been removed.

### Root Cause

The user had management-plane read access to the Azure resource but did not have the required data-plane permission to read Blob Storage data.

### Resolution

The `Storage Blob Data Reader` role was restored using the `Cloud-Lab-Admins` Microsoft Entra ID group.

This restored Blob read access without granting unnecessary write or delete permissions.

### Lesson

Azure management-plane and data-plane permissions are separate.

`Reader` allows an identity to view Azure resources and configuration.

`Storage Blob Data Reader` allows an identity to read and list Blob Storage data.

Using the data-reader role instead of a contributor role also follows the principle of least privilege.

---

## Troubleshooting Methodology

Across the scenarios, I followed a layered troubleshooting process:

**DNS → Network Path → Port Connectivity → Security Controls → Identity → Authorization → Application**

This approach helped isolate the failing layer before making configuration changes.
