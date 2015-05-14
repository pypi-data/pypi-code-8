from botocore.session import get_session

session = get_session()

client = session.create_client("route53", "eu-west-1")

client.change_resource_record_sets(
    HostedZoneId="1111",
    ChangeBatch={
        "Changes": [{"Action": "UPSERT", "ResourceRecordSet": {"Name": "www", "Type": "A"}}],
    },
)

