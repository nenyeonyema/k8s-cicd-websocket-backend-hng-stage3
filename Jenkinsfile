pipe                                                                                   pipeline {

    agent any

    environment {
        DOCKER_IMAGE = "nenyeonyema/helloworld"
        DOCKER_TAG = "latest"
        KUBE_CONFIG = "$HOME/.kube/config"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/your-repo/k8s-cicd-websocket-backend-hng-stage3.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE:$DOCKER_TAG ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh "docker login -u your-dockerhub-username -p your-dockerhub-password"
                    sh "docker push $DOCKER_IMAGE:$DOCKER_TAG"
                }
            }
        }

        stage('Deploy to Kubernetes Test Environment') {
            steps {
                script {
                    sh "kubectl apply -f test-deployment.yaml"
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

        stage('Deploy to Production') {
            when {
                expression { return currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    sh "kubectl apply -f deployment.yaml"
                    sh "kubectl apply -f service.yaml"
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
}
