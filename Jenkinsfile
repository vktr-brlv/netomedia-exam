DEFAULTS              = [:] as HashMap
DEFAULTS.gcpProjectId = "${env.GCP_DEFAULT_PROJECT_ID}"
DEFAULTS.gcpGcr       = "gcr.io/${env.GCP_DEFAULT_PROJECT_ID}"
DEFAULTS.gcpCredsId   = "${env.GCP_DEFAULT_PROJECT_ID}"
DEFAULTS.imageName    = "app"
DEFAULTS.imageTag     = 'latest'
DEFAULTS.imageRelease = '0.1'

def label = "helm-image-slave-${UUID.randomUUID().toString()}"
podTemplate(
    cloud: 'kubernetes',
    label: label,
    containers: [
        containerTemplate(
            name: 'docker',
            image: 'docker:git',
            alwaysPullImage: true,
            command: 'cat',
            ttyEnabled: true
        ),
        containerTemplate(
            name: 'helm',
            image: "${DEFAULTS.gcpGcr}/helm-slave",
            alwaysPullImage: true,
            command: 'cat',
            ttyEnabled: true
        )
     ],
    volumes: [hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')]
) {

    node(label) {
        container('docker'){
            stage('checkout'){
                echo 'In checkout stage'
                checkout scm
                gitHash = sh (
                    script: 'git rev-parse --short HEAD',
                    returnStdout: true
                )
            }

            stage('build'){
                echo 'In build stage'
                wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm']) {
                    Img = docker.build(
                        "${DEFAULTS.gcpProjectId}/${DEFAULTS.imageName}:${DEFAULTS.imageTag}",
                        "-f Dockerfile ./"
                    )
                }
            }

            stage('test'){
                echo 'In test stage'
            }

            stage('push'){
                echo 'In push stage'
                docker.withRegistry('https://gcr.io', "gcr:${DEFAULTS.gcpProjectId}") {
                    Img.push("${DEFAULTS.imageRelease}.${env.BUILD_NUMBER}-${gitHash}")
                    Img.push("${DEFAULTS.imageTag}")
                }
            }
        }
        container('helm'){
            stage('deploy'){
                echo 'Deploy app to gke'
                dir('helm'){
                    withCredentials([file(credentialsId: "creds-k8s", variable: 'KUBECONFIG'),\
                                     file(credentialsId: "creds-gcp-sa-jenkins", variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        sh 'helm upgrade -i app ./app'
                     }
                }
            }
        }
    }
}