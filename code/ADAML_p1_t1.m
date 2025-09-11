clear all
close all
clc

%% Load Spectral_Soft_Sensor_1.csv properly
file = '../data/Spectral_Soft_Sensor_1.csv';

% Step 1: Read everything as cell array
raw = readcell(file);

% Step 2: Extract variable names (1st row, from 2nd column onward)
headers = raw(1, 2:end);

% Fix problematic headers: numeric or empty to string
for i = 1:length(headers)
    if isnumeric(headers{i})
        headers{i} = sprintf('band_%d', headers{i});
    elseif isempty(headers{i}) || (ischar(headers{i}) && all(isspace(headers{i})))
        headers{i} = sprintf('var_%d', i);
    end
end

% Step 3: Convert data section to numeric (rows 2:end, columns 2:end)
raw_data = raw(2:end, 2:end);
data = cellfun(@str2double, raw_data);  % non-numeric becomes NaN

% Step 4: Create table
T1 = array2table(data, 'VariableNames', headers);

% Step 5: Save cleaned matrix
save('X1_cleaned.mat', 'T1');

% Step 6: Output info
[n_obs, n_vars] = size(T1);
fprintf('✅ Final data loaded: %d rows, %d variables (excluding index column)\n', n_obs, n_vars);

% Step 7: Show first 10x10 block
disp(T1(1:10, 1:10));

% 1. Eksik değer analizi
missing_counts = sum(ismissing(T1));
total_missing = sum(missing_counts);
fprintf('Total missing values in dataset: %d\n', total_missing);

% 2. En çok eksik olan sütunları göster
[sorted, idx] = sort(missing_counts, 'descend');
disp('Top 10 variables with most missing values:');
disp(table(T1.Properties.VariableNames(idx(1:10))', sorted(1:10)', ...
    'VariableNames', {'Variable', 'MissingValues'}));