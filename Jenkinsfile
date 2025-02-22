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

        stage('Run Tests') {
            steps {
                script {
                    sh "kubectl exec -it test-pod -- python test_helloworld.py"
                }
            }
        }


        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: "${KUBE_CONFIG_ID}", variable: 'KUBECONFIG')]) {
                    sh '''
                    export KUBECONFIG=$KUBECONFIG
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    '''
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
