import sys
sys_fields_to_ignore_set=set(["ArchivedDate","LastViewedDate","LastPublishedDate","LastReferencedDate","FirstPublishedDate","IsDeleted","CurrencyIsoCode","CreatedDate","CreatedById","LastModifiedDate","LastModifiedId","SystemModstamp","ArchivedById","ArticleArchivedById","ArticleArchivedDate"])
def write_count_soql(objectToQuery):
    count_SOQL = f"SELECT count(Id) FROM {objectToQuery}"
    with open(".tmp/countSOQL.txt", "w") as f:
        f.write(count_SOQL)

def write_actual_soql(allfields, objectToQuery):
    csFields = ",".join(allfields)
    actual_Soql = f"SELECT {csFields} FROM {objectToQuery}"
    with open(".tmp/actualSOQL.txt", "w") as f:
        f.write(actual_Soql)


if __name__ == "__main__":
    fileNameToRead = sys.argv[1]
    objectToQuery = sys.argv[2]
    print(fileNameToRead)
    print(sys_fields_to_ignore_set)
    with open(fileNameToRead, "r") as f:
        csv_fields_set=set(f.readline().split(','))
    all_fields_to_query = csv_fields_set - sys_fields_to_ignore_set
    print(all_fields_to_query)
    write_count_soql(objectToQuery)
    write_actual_soql(all_fields_to_query, objectToQuery)
    
    sys.exit()