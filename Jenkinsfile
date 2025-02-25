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

        stage('Deploy Test Job to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                    sh '''
                    export KUBECONFIG=$KUBECONFIG

                    # Ensure previous test job is deleted before applying new one
                    kubectl delete job -n testing test-job --ignore-not-found=true

                    # Apply the Kubernetes job to run tests
                    kubectl apply -f k8s/test-job.yml
                    '''
                }
            }
        }

        stage('Run Test') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                    sh '''
                    export KUBECONFIG=$KUBECONFIG

                    echo "Waiting for test-job to complete..."
                    kubectl wait --for=condition=complete --timeout=120s job/test-job -n testing || exit 1

                    echo "Fetching test logs..."
                    kubectl logs -n testing job/test-job
                    '''
                }
            }
        }


        stage('Deploy to Production on Kubernetes') {
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

    post {
        always {  // Cleanup only if the pipeline fails
            withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                sh '''
                export KUBECONFIG=$KUBECONFIG
                echo "Pipeline failed! Cleaning up test job..."
                kubectl delete job -n testing test-job || true
                '''
            }
        }
        failure {
            echo "Pipeline failed!"
        }

        success {
            echo "Deployment successful!"
        }
    }

}
