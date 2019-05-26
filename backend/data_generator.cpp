#include<bits/stdc++.h>
#define fo(i, x, y) for (int i = x; i <= y; ++i)
using namespace std;

int main(){
	srand(time(0));
	
	// Annoucement
	fo(i, 1, 50000){
		int uid = rand() % 3;
		if (uid == 0) uid = 3;
		else if (uid == 2) uid = 10;
		printf("insert into announcement (title, description, uid, publish_time) values ('Announcement %d', 'Announcement %d', %d, sysdate());\n", i, i, uid);
	}

	// UserGroup
	fo(i, 1, 10000){
		printf("insert into user_group (group_name, description) values ('Group__random__%d', 'Group %d (random generated)');\n", i, i);
	}

	// UserInGroup
	fo(i, 1, 20000){
		printf("insert into user_in_group (uid, gid) values (%d, %d);\n", rand() * rand() % 50000 + 11, rand() % 9000 + 10);
	}

	// Task
	fo(i, 1, 10000){
		if (i % 100 == 1) printf("insert into task (task_name, description, deadline) values ");
		printf("('Task %d', 'Task__random__%d', sysdate())", i, i);
		if (i % 100 == 0) printf(";\n");
		else printf(", ");
	}

	// Problem
	fo(i, 1, 20000){
		if (i % 100 == 1) printf("insert into problem (title, description, level, visible) values ");
		printf("('Sample Problem (%d)', concat_ws(char(10), '## Sample A + B Problem', '> Function: add(a, b)'), %d, 1)", i, rand() % 3 + 1);
		if (i % 100 == 0) printf(";\n");
		else printf(", ");
	}

	// Task For UserGroup
	fo(i, 1, 30000){
		if (i % 100 == 1) printf("insert into task_for_usergroup (task_id, gid) values ");
		printf("(%d, %d)", rand() * rand() % 9000 + 4, rand() * rand() % 10000 + 3);
		if (i % 100 == 0) printf(";\n");
		else printf(", ");
	}
	
	// Problem In Task
	fo(i, 1, 50000){
		if (i % 100 == 1) printf("insert into problem_in_task (task_id, pid) values ");
		printf("(%d, %d)", rand() * rand() % 9000 + 4, rand() * rand() % 20000 + 6);
		if (i % 100 == 0) printf(";\n");
		else printf(", ");
	}

	// Tag Of Problem
	fo(i, 1, 15000){
		printf("insert into tag_of_problem (tag_id, pid) values (%d, %d);\n", rand() % 3 + 1, rand() * rand() % 20000 + 6);
	}

	// Testset and Test
	int test_id = 10;
	int testset_id = 9;
	fo(i, 1, 20000){
		++testset_id;
		if (rand() & 1){
			printf("insert into testset (full_score) values (30);\n");
			fo(j, 1, 3){
				++test_id;
				int x = rand() % 100, y = rand() % 100;
				printf("insert into test (score, code) values (10, 'assert add(%d, %d) == %d');\n", x, y, x + y);
				printf("insert into test_in_testset (test_id, testset_id) values (%d, %d);\n", test_id, testset_id);
			}
			printf("update problem set testset_id = %d where pid = %d;\n", testset_id, rand() * rand() % 20000 + 6);
		}
		else
			printf("insert into testset (full_score) values (0);\n");
	}
}