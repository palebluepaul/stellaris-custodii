#!/bin/bash
echo "sound = {" > output/working/updated_working.asset
echo "	name = \"advisor_notification_colony_ship_destroyed_03\"" >> output/working/updated_working.asset
echo "	file = \"vo/custodii-advisor/advisor_notification_colony_ship_destroyed_03.wav\"" >> output/working/updated_working.asset
echo "}" >> output/working/updated_working.asset

while read -r sound_id; do
  echo "" >> output/working/updated_working.asset
  echo "sound = {" >> output/working/updated_working.asset
  echo "	name = \"$sound_id\"" >> output/working/updated_working.asset
  echo "	file = \"vo/custodii-advisor/$sound_id.wav\"" >> output/working/updated_working.asset
  echo "}" >> output/working/updated_working.asset
done < output/working/extracted_sound_ids.txt 