TARGET_DIR="subscriber/output/latency_log"

cat $TARGET_DIR/*.txt | awk '{ total += $1; count++ } END { if (count > 0) print "Average Latency:", total/count, "ms"; else print "No data found." }'