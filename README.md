# argo-exporter

# Brief introduction
ArgoCD Prometheus exporter for reading the application tags and showing deployment drift from the `now()` time.

The idea of this exporter is to bring to Prometheus metrics which can show the cadance of deployments for GitOps oriented companies.

It exports the current Docker `image tag`, the `Application` from the ArgoCD CRD, and the `deployedAt` from the history of the application.

# How it works
It does 1+n where n=number of applications deployed via ArgoCD `Application` CRDs. The first request is getting the application names, and the other request are traversing via the ArgoCD API the needed data.

# How to run
Its built on Python, so just running `python main.py` gets you the exporter up and running, but before that you need to set the configuration described in the next section. The exporter is available on port `8000`.

# Configuration

`ARGOCD_API_ENDPOINT` - your `in-cluster` ArgoCD Server deployment endpoint. Usually its `svc/argocd-server` on port `8080` in the `argocd` namespace. Mind that the default installation of ArgoCD runs on `https://` but with self-signed certificate.

`ARGOCD_API_TOKEN` - token for the API of the ArgoCD Server. This token can be obtained via the following command after you authenticate your `argocd` CLI: `argocd account generate-token --account admin`
