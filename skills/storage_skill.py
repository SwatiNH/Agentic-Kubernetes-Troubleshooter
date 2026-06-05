"""
Storage Skill - Kubernetes Storage Analysis

This skill analyzes persistent volumes, persistent volume claims, storage classes,
and disk I/O in a Kubernetes cluster. It detects storage misconfigurations,
capacity issues, and performance problems.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class StorageIssue:
    """Represents a storage-related issue"""
    issue_id: str
    type: str  # UnboundPVC, StorageClassNotFound, LowDiskSpace, IOIssue, etc.
    resource_name: str
    namespace: str
    severity: str  # critical, high, medium, low
    description: str
    resource_type: str = "PVC"  # PVC, PV, StorageClass, Node
    current_state: str = None
    storage_class: str = None
    capacity: str = None
    used_space: str = None
    affected_pods: List[str] = None
    events: List[str] = None
    recommendations: List[str] = None
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        if self.events is None:
            self.events = []
        if self.affected_pods is None:
            self.affected_pods = []
        if self.recommendations is None:
            self.recommendations = []


@dataclass
class StorageMetrics:
    """Cluster-wide storage metrics"""
    total_pvs: int
    bound_pvs: int
    total_pvcs: int
    bound_pvcs: int
    unbound_pvcs: int
    total_storage_classes: int
    total_storage_capacity: float  # GB
    total_storage_used: float  # GB
    storage_utilization_percent: float
    nodes_with_low_disk: int
    nodes_low_disk_threshold: str  # e.g., "10%"
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


class StorageSkill(ABC):
    """
    Storage Skill Implementation
    
    Analyzes:
    - PersistentVolume (PV) provisioning and binding
    - PersistentVolumeClaim (PVC) binding and satisfaction
    - StorageClass configurations
    - Volume mount failures
    - Disk space utilization
    - I/O performance issues
    - Storage quota violations
    """

    def __init__(self, k8s_client):
        self.k8s_client = k8s_client
        self.name = self.__class__.__name__
        self.skill_type = "storage"
        self.issues = []
        self.metrics = {}

    def analyze(self) -> Dict[str, Any]:
        """
        Execute comprehensive storage analysis
        
        Returns:
            Dictionary containing:
            - issues: List of StorageIssue objects
            - metrics: StorageMetrics object
            - recommendations: List of actionable recommendations
        """
        self.issues = []
        
        # Run analysis methods
        self._analyze_pvc_status()
        self._analyze_pv_status()
        self._analyze_storage_classes()
        self._analyze_volume_mounts()
        self._analyze_disk_usage()
        self._calculate_metrics()
        
        return {
            "skill": self.name,
            "status": "completed",
            "issues": [asdict(issue) for issue in self.issues],
            "metrics": asdict(self.metrics),
            "recommendations": self._generate_recommendations(),
            "timestamp": datetime.utcnow().isoformat()
        }

    def _analyze_pvc_status(self):
        """
        Analyze PersistentVolumeClaim status
        
        Detects:
        - Unbound PVCs (pending provisioning)
        - PVCs with missing StorageClass
        - PVC provisioning failures
        - PVCs in failed state
        """
        # Placeholder: In actual implementation, query Kubernetes API
        # pvcs = self.k8s_client.list_namespaced_persistent_volume_claim(namespace="all")
        # for pvc in pvcs:
        #     if pvc.status.phase == "Pending":
        #         if not pvc.spec.storage_class_name:
        #             # Issue: No storage class specified
        #         else:
        #             # Issue: Provisioning pending
        
        pass

    def _analyze_pv_status(self):
        """
        Analyze PersistentVolume status
        
        Detects:
        - Unbound PVs available for provisioning
        - PVs in failed state
        - PV reclaim policy issues
        - PV access mode mismatches
        """
        # Placeholder: In actual implementation
        # pvs = self.k8s_client.list_persistent_volume()
        # for pv in pvs:
        #     if pv.status.phase == "Available":
        #         pass  # May be ok, but could indicate sizing issue
        #     if pv.status.phase == "Failed":
        #         # Issue: PV in failed state
        
        pass

    def _analyze_storage_classes(self):
        """
        Analyze StorageClass configurations
        
        Detects:
        - Missing default StorageClass
        - StorageClasses with invalid provisioners
        - Deprecated or misconfigured StorageClasses
        - Volume binding mode issues
        """
        # Placeholder: In actual implementation
        # storage_classes = self.k8s_client.list_storage_class()
        # for sc in storage_classes:
        #     if not sc.provisioner or sc.provisioner == "":
        #         # Issue: Invalid provisioner
        
        pass

    def _analyze_volume_mounts(self):
        """
        Analyze pod volume mounts and bindings
        
        Detects:
        - Failed volume mounts
        - Pods unable to mount volumes
        - Volume mount permission issues
        - Duplicate mount paths
        """
        # Placeholder: In actual implementation
        # pods = self.k8s_client.list_pod_for_all_namespaces()
        # for pod in pods:
        #     for volume_mount in pod.spec.volumes:
        #         if pod.status.phase != "Running":
        #             # Potential mount issue
        
        pass

    def _analyze_disk_usage(self):
        """
        Analyze disk usage and capacity
        
        Detects:
        - Nodes running low on disk space
        - High disk utilization on volumes
        - Disk space trending to full
        - Storage quota violations
        """
        # Placeholder: In actual implementation
        # nodes = self.k8s_client.list_node()
        # for node in nodes:
        #     # Get disk metrics from kubelet or metrics-server
        #     disk_available = node.status.allocatable.get("ephemeral-storage")
        #     disk_pressure = any(c.type == "DiskPressure" and c.status == "True" 
        #                        for c in node.status.conditions)
        
        pass

    def _calculate_metrics(self):
        """Calculate cluster-wide storage metrics"""
        # Placeholder: Aggregate metrics from analysis
        self.metrics = StorageMetrics(
            total_pvs=0,
            bound_pvs=0,
            total_pvcs=0,
            bound_pvcs=0,
            unbound_pvcs=0,
            total_storage_classes=0,
            total_storage_capacity=0.0,
            total_storage_used=0.0,
            storage_utilization_percent=0.0,
            nodes_with_low_disk=0,
            nodes_low_disk_threshold="10%"
        )

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on findings"""
        recommendations = []
        
        if any(issue.severity == "critical" for issue in self.issues):
            recommendations.append("Address critical storage issues immediately to prevent data loss")
        
        # Add more recommendations based on issue types
        issue_types = set(issue.type for issue in self.issues)
        
        if "UnboundPVC" in issue_types:
            recommendations.append("Create missing StorageClasses or ensure provisioners are configured")
        
        if "LowDiskSpace" in issue_types:
            recommendations.append("Expand storage capacity or delete unused data")
        
        if "IOIssue" in issue_types:
            recommendations.append("Investigate I/O performance bottlenecks and consider performance-tier storage")
        
        return recommendations

    def get_issues(self) -> List[Dict[str, Any]]:
        """Return all identified storage issues"""
        return [asdict(issue) for issue in self.issues]

    def get_metrics(self) -> Dict[str, Any]:
        """Return storage metrics"""
        return asdict(self.metrics) if self.metrics else {}
