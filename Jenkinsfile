pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nenyeonyema/helloworld:latest"
        DOCKER_CRED_ID = 'docker-login-cred'
        KUBE_CONFIG_ID = 'kubeconfig-cred'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/nenyeonyema/k8s-cicd-websocket-backend-hng-stage3'
            }
        }

        stage('Docker Build & Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-login-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker build -t nenyeonyema/helloworld:latest .
                    docker push nenyeonyema/helloworld:latest
                    '''
                }
            }
        }

        stage('Deploy Test Pod') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                    sh '''
                    export KUBECONFIG=$KUBECONFIG
                    kubectl apply -f k8s/test-pod.yml
                    '''
                }
            }
        }

        stage('Run Tests in Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                    sh '''
                    export KUBECONFIG=$KUBECONFIG
                    which kubectl  # Check if kubectl is accessible
                    kubectl exec test-runner -n testing -- python test_helloworld.py
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: "${KUBE_CONFIG_ID}", variable: 'KUBECONFIG')]) {
                    sh '''
                    export KUBECONFIG=$KUBECONFIG
                    kubectl apply -f k8s/deployment.yml
                    kubectl apply -f k8s/service.yml
                    '''
                }
            }
        }

    }
}

    post {
        failure {  // Only delete if pipeline fails
            withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                sh '''
                export KUBECONFIG=$KUBECONFIG
                echo "Pipeline failed! Cleaning up test pod..."
                kubectl delete pod -n testing test-runner || true
                '''
            }
        success {
            echo "Deployment successful!"
        }
    }
}
