# 🚀 Kubernetes Namespace, ResourceQuota & LimitRange Setup

## 📌 Step-by-Step Deployment

---

## ✅ Step 1: Create YAML file

Create a file:

bash
vim dev-namespace.yml

Paste the following YAML:

apiVersion: v1
kind: Namespace
metadata:
  name: dev

---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: app-resource-quota
  namespace: dev
spec:
  hard:
    pods: "10"
    requests.cpu: "3"
    requests.memory: 2Gi
    limits.cpu: "4"
    limits.memory: 4Gi

---
apiVersion: v1
kind: LimitRange
metadata:
  name: app-limit-range
  namespace: dev
spec:
  limits:
    - default:
        cpu: "500m"
        memory: "512Mi"
      defaultRequest:
        cpu: "250m"
        memory: "256Mi"
      type: Container
✅ Step 2: Apply configuration
kubectl apply -f dev-namespace.yml
✅ Step 3: Verify Namespace
kubectl get ns

You should see:

dev
✅ Step 4: Verify ResourceQuota
kubectl get resourcequota -n dev

Detailed view:

kubectl describe resourcequota app-resource-quota -n dev
✅ Step 5: Verify LimitRange
kubectl get limitrange -n dev

Detailed view:

kubectl describe limitrange app-limit-range -n dev
📌 Important Notes (VERY IMPORTANT for interviews)
🔹 Namespace
Logical isolation in Kubernetes
All resources (pods, services) will be created inside dev
🔹 ResourceQuota (Cluster Safety 🚧)

Limits total resources in the namespace:

Resource	Limit
Pods	10
CPU Requests	3 cores
Memory Requests	2Gi
CPU Limits	4 cores
Memory Limits	4Gi

👉 If exceeded → Pod creation will fail

🔹 LimitRange (Default Values ⚙️)

Applies defaults when not specified in Pod:

Type	CPU	Memory
Request	250m	256Mi
Limit	500m	512Mi

👉 If developer doesn’t define resources → Kubernetes assigns these automatically

🧪 Real-Time Behavior Examples
❌ Case 1: No resources defined in Pod
containers:
- name: app
  image: nginx

👉 Automatically becomes:

requests:
  cpu: 250m
  memory: 256Mi
limits:
  cpu: 500m
  memory: 512Mi
❌ Case 2: Exceed ResourceQuota

If you try:

replicas: 20

👉 Error:

exceeded quota: app-resource-quota
🧪 Step 6: Test with Sample Pod
kubectl run test-pod \
  --image=nginx \
  -n dev

Check:

kubectl describe pod test-pod -n dev

👉 You’ll see default CPU/memory applied from LimitRange

💡 Pro Tips (DevOps / Interview)

✔ Always combine:

Namespace
ResourceQuota
LimitRange

👉 Ensures:

Multi-tenant isolation
Resource control
Fair usage
🧹 Cleanup
kubectl delete -f dev-namespace.yml

---

If you want, I can also:
- Convert this into **GitHub README style with badges**
- Add **architecture diagram**
- Or turn this into a **Helm chart structure** 🚀
