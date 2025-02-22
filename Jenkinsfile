pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nenyeonyema/helloworld:latest"
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
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker build -t $DOCKER_IMAGE .
                        docker push $DOCKER_IMAGE
                    """
                }
            }
        }

        stage('Deploy to Kubernetes Test Environment') {
            steps {
                script {
                    sh "kubectl apply -f k8s/test-pod.yml"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh "kubectl exec -it test-pod -- python test_helloworld.py"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                    sh """
                        export KUBECONFIG=$KUBECONFIG
                        kubectl apply -f k8s/deployment.yml
                        kubectl apply -f k8s/service.yml
                    """
                }
            }
        }
    }
}

    post {
        failure {
            echo "Pipeline failed. Check logs."
        }
        success {
            echo "Deployment successful!"
        }
    }
