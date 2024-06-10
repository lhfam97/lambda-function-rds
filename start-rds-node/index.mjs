import AWS from "aws-sdk";

function startRdsAll() {
  const region = process.env.REGION;
  const key = process.env.KEY;
  const value = process.env.VALUE;

  const client = new AWS.RDS({ region });

  client.describeDBInstances((err, data) => {
    if (err) {
      console.log(err, err.stack);
      return;
    }

    data.DBInstances.forEach((instance) => {
      const arn = instance.DBInstanceArn;
      client.listTagsForResource({ ResourceName: arn }, (err, tagData) => {
        if (err) {
          console.log(err, err.stack);
          return;
        }
        // Check if the RDS instance is part of the Auto-Shutdown group.
        if (tagData.TagList.length === 0) {
          console.log(
            `DB Instance ${instance.DBInstanceIdentifier} is not part of dev environment`
          );
        } else {
          tagData.TagList.forEach((tag) => {
            if (tag.Key === key && tag.Value === value) {
              switch (instance.DBInstanceStatus) {
                case "available":
                  console.log(
                    `${instance.DBInstanceIdentifier} DB instance is already available`
                  );
                  break;
                case "stopped":
                  client.startDBInstance(
                    { DBInstanceIdentifier: instance.DBInstanceIdentifier },
                    (err) => {
                      if (err) {
                        console.log(err, err.stack);
                        return;
                      }
                      console.log(
                        `Started DB Instance ${instance.DBInstanceIdentifier}`
                      );
                    }
                  );
                  break;
                case "starting":
                  console.log(
                    `DB Instance ${instance.DBInstanceIdentifier} is already in starting state`
                  );
                  break;
                case "stopping":
                  console.log(
                    `DB Instance ${instance.DBInstanceIdentifier} is in stopping state. Please wait before starting`
                  );
                  break;

                default:
                  break;
              }
            } else if (
              (tag.Key !== key && tag.Value !== value) ||
              tag.Key.length === 0 ||
              tag.Value.length === 0
            ) {
              console.log(
                `DB instance ${instance.DBInstanceIdentifier} is not part of dev environment`
              );
            }
          });
        }
      });
    });
  });
}

export function lambdaHandler(event, context) {
  startRdsAll();
}
