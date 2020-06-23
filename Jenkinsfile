DEFAULTS              = [:] as HashMap
DEFAULTS.gcpProjectId = "${env.GCP_DEFAULT_PROJECT_ID}"
DEFAULTS.gcpGcr       = "gcr.io/${env.GCP_DEFAULT_PROJECT_ID}"
DEFAULTS.gcpCredsId   = "${env.GCP_DEFAULT_PROJECT_ID}"
DEFAULTS.imageName    = "jenkins-slave"
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
                dir('app') {
                    wrap([$class: 'AnsiColorBuildWrapper', 'colorMapName': 'XTerm']) {
                        Img = docker.build(
                            "${DEFAULTS.gcpProjectId}/${DEFAULTS.imageName}:${DEFAULTS.imageTag}",
                            "-f Dockerfile ./"
                        )
                    }
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
    }
}