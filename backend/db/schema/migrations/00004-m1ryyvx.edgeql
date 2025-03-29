CREATE MIGRATION m1ryyvxuknmgfaabnlgfjxfrzobtcf5227ksrw4is74ukplzrk2o6a
    ONTO m1h3lnmq4nlzhcbavrd3sanq6su7dilaeee3ip2262jla465hdk2aa
{
  ALTER TYPE default::reply RENAME TO default::Reply;
  ALTER TYPE default::Reply {
      CREATE LINK parent_reply: default::Reply;
  };
};
