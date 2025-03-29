CREATE MIGRATION m1sg5xzfaderbvmluplpcbkoo3szgpplbkp2ciwzof2cebaxwtrtgq
    ONTO initial
{
  CREATE EXTENSION postgis VERSION '3.5';
  CREATE FUTURE simple_scoping;
  CREATE TYPE default::rant {
      CREATE REQUIRED PROPERTY created_at: std::datetime;
      CREATE REQUIRED PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY geom: std::json;
      CREATE REQUIRED PROPERTY title: std::str;
      CREATE REQUIRED PROPERTY vote_count: std::int32;
  };
};
