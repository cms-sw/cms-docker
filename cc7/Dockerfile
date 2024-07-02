FROM @BASE_IMAGE_NAME@
LABEL maintainer="CMS Build"
LABEL name="CMS Worker Node on EL"

RUN yum --disablerepo=base --disablerepo=updates --disablerepo=extras install -y \
    jq vim &&\
    update-ca-trust &&\
    yum clean all &&\
    echo "Timestamp: @BUILD_DATE@"   > /image-build-info.txt

LABEL build-date="@BUILD_DATE@"
